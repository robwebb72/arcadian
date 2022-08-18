import random
import sys
from random import randint
from typing import List

import pygame

EMITTER_CREATED = 0
EMITTER_RUNNING = 1
EMITTER_STOPPED = 2

PARTICLE_ALIVE = 0
PARTICLE_DEAD = 1


class ParticleType:
    def __init__(self, lifetime_fn, weighting: int, colour_fn, size_fn, direction_fn, offset_fn, speed_fn):
        self._weighting = weighting
        self._lifetime_fn = lifetime_fn
        self._colour_fn = colour_fn
        self._size_fn = size_fn
        self._direction_fn = direction_fn
        self._offset_fn = offset_fn
        self._speed_fn = speed_fn

    def _vector_fn(self):
        return self._direction_fn(self._speed_calc())

    def _speed_calc(self):
        return self._speed_fn()


class Particle:
    def __init__(self):
        self._state: int = PARTICLE_DEAD
        self._lifetime_value = 0
        self._lifetime_initial_value = 1

    def create_from_type(self, particle_type: ParticleType):
        self._lifetime_initial_value = particle_type._lifetime_fn()
        self._lifetime_value = self._lifetime_initial_value
        if self._lifetime_initial_value == 0:
            self._state = PARTICLE_DEAD
            return
        self._size_fn = particle_type._size_fn
        self._vector_value: pygame.math.Vector2 = pygame.math.Vector2(particle_type._vector_fn())
        self._state = PARTICLE_ALIVE
        self._offset = particle_type._offset_fn()
        self._colour_fn = particle_type._colour_fn

    def set_position(self, position: pygame.math.Vector2):
        self._position = position + self._offset

    def _update_lifetime(self, dt_sec: float) -> None:
        if self._state == PARTICLE_DEAD:
            return
        self._lifetime_value -= dt_sec
        self._lifetime_ratio = 1 - (self._lifetime_value / self._lifetime_initial_value)
        if self._lifetime_ratio >= 1:
            self._state = PARTICLE_DEAD
            return

    def update(self, dt_sec: float) -> None:
        self._update_lifetime(dt_sec)
        if self._state == PARTICLE_DEAD:
            return

        delta = pygame.math.Vector2(self._vector_value.x * dt_sec, self._vector_value.y * dt_sec)
        self._position += delta

    def colour(self) -> int:
        return self._colour_fn(self._lifetime_ratio)

    def size(self) -> int:
        return self._size_fn(self._lifetime_ratio)

    def get_draw_info(self):
        return (self._position, self.size(), self.colour())


class ParticleEmitter:
    def __init__(
        self,
        nparticles: int,
        particle_types: List[ParticleType],
        position: pygame.math.Vector2,
        perpetual: bool = False,
    ):
        self._state = EMITTER_CREATED
        self._particle_type_weighting: int = self._calc_weighting_total(particle_types)
        self.position = position
        self._particle_types = particle_types
        self._particles: List[Particle] = self._create_particles(nparticles)
        self._perpetual = perpetual

    def update_position(self, position: pygame.math.Vector2):
        self._position = position

    def _calc_weighting_total(self, particle_types: List[ParticleType]) -> int:
        weighting_total: int = 0
        for particle_type in particle_types:
            weighting_total += particle_type._weighting
        return weighting_total

    def _create_particle(self):
        particle_type = self._get_particle_type()
        particle = Particle()
        particle.create_from_type(particle_type)
        particle.set_position(self.position)
        return particle

    def _create_particles(self, nparticles: int) -> List[Particle]:
        particles = []
        for _ in range(nparticles):
            particle = self._create_particle()
            particles.append(particle)
        return particles

    def _get_particle_type(self) -> ParticleType:
        random_value: int = randint(0, self._particle_type_weighting)
        return self._find_particle_type_by_weighting(random_value)

    def _find_particle_type_by_weighting(self, value: int):
        target_weight = value
        i: int = 1

        current_type = self._particle_types[0]
        weighting_running_total: int = self._particle_types[0]._weighting

        while i < len(self._particle_types) and target_weight > weighting_running_total:
            current_type = self._particle_types[i]
            i += 1
            weighting_running_total += current_type._weighting
        return current_type

    def turn_on(self, set_to_on: bool):
        self._state = EMITTER_RUNNING if set_to_on else EMITTER_STOPPED

    def update(self, dt_sec: float) -> None:
        if self._state != EMITTER_RUNNING:
            return
        [particle.update(dt_sec) for particle in self._particles]

        for particle in self._particles:
            if particle._state == PARTICLE_DEAD and self._perpetual:
                random_value = randint(0, self._particle_type_weighting)
                particle_type = self._find_particle_type_by_weighting(random_value)
                particle = particle_type.create_particle()
            else:
                particle.update(dt_sec)
        if self._are_any_particles_active() or self._perpetual:
            pass
        else:
            self._state = EMITTER_STOPPED

    def _are_any_particles_active(self):
        for particle in self._particles:
            if particle._state == PARTICLE_ALIVE:
                return True
        return False

    def set_state(self, state: int) -> None:
        self._state = state

    def draw(self, screen: pygame.Surface) -> None:
        if self._state != EMITTER_RUNNING:
            return
        for particle in self._particles:
            if particle._state == PARTICLE_ALIVE:
                size = particle.size()
                pygame.draw.rect(
                    screen, particle.colour(), (int(particle._position.x), int(particle._position.y), size, size)
                )


lifetime_fn = lambda x, y: x + random.random() * (y - x)
size_fn = lambda x: 1 if x > 0.5 else 2
white_fn = lambda x: (255, 255, 255)
red_fn = lambda x: (255, 0, 0)
yellow_fn = lambda x: (255, 255, 0)
rand_speed_fn = lambda x: x * (0.1 + random.random() * 0.9)
offset_origin_fn = lambda: pygame.math.Vector2(0, 0)
vector_circular_unit_vector_fn = lambda x: pygame.math.Vector2(x, 0).rotate(random.random() * 360)
vector_2_fn = lambda x: pygame.math.Vector2(100, 0)

explosion_particle1 = ParticleType(
    lambda: lifetime_fn(0.4, 0.6),
    100,
    lambda x: (255, 0, 0),
    lambda x: 2,
    vector_circular_unit_vector_fn,
    offset_origin_fn,
    lambda: rand_speed_fn(100),
)

explosion_particle2 = ParticleType(
    lambda: lifetime_fn(0.2, 0.4),
    100,
    lambda x: (255, 255, 0),
    lambda x: 2,
    vector_circular_unit_vector_fn,
    offset_origin_fn,
    lambda: rand_speed_fn(40),
)

explosion_particle3 = ParticleType(
    lambda: lifetime_fn(0.6, 0.8),
    80,
    lambda x: (255, 255, 255),
    lambda x: 2,
    vector_circular_unit_vector_fn,
    offset_origin_fn,
    lambda: rand_speed_fn(2000),
)

explosion_particle4 = ParticleType(
    lambda: lifetime_fn(0.2, 0.4),
    20,
    lambda x: (255, 255, 255),
    lambda x: 6,
    vector_circular_unit_vector_fn,
    offset_origin_fn,
    lambda: rand_speed_fn(500),
)

explosion_particle5 = ParticleType(
    lambda: lifetime_fn(0.2, 0.4),
    5,
    lambda x: (255, 0, 0),
    lambda x: 6,
    vector_circular_unit_vector_fn,
    offset_origin_fn,
    lambda: rand_speed_fn(500),
)

explosion_types = [explosion_particle1, explosion_particle2, explosion_particle3, explosion_particle4, explosion_particle5]

class ParticleExplosion:
    def __init__(self, position: pygame.math.Vector2) -> None:
        self._emitter = ParticleEmitter(300, explosion_types, position)
    
    def turn_on(self):
        self._emitter.turn_on(True)

    def draw(self, screen):
        self._emitter.draw(screen)
    
    def update(self, dt_sec:float):
        self._emitter.update(dt_sec)