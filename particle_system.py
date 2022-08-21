from random import randint
from typing import List

import pygame

EMITTER_CREATED = 0
EMITTER_RUNNING = 1
EMITTER_STOPPED = 2

PARTICLE_ALIVE = 0
PARTICLE_DEAD = 1


class ParticleType:
    def __init__(
        self,
        lifetime_fn,
        weighting: int,
        colour_fn,
        size_fn,
        direction_fn,
        offset_fn,
        speed_fn,
    ):
        self._weighting = weighting
        self._lifetime_fn = lifetime_fn
        self._colour_fn = colour_fn
        self._size_fn = size_fn
        self._direction_fn = direction_fn
        self._offset_fn = offset_fn
        self._speed_fn = speed_fn

    def _velocity_fn(self):
        return self._direction_fn(self._speed_fn())


class Particle:
    def __init__(self, particle_type, position):
        self.create_from_type(particle_type, position)

    def create_from_type(self, particle_type: ParticleType, position):
        self._lifetime_total = particle_type._lifetime_fn()
        if self._lifetime_total == 0:
            self._state = PARTICLE_DEAD
            return
        self._lifetime_current = self._lifetime_total
        self._size_fn = particle_type._size_fn
        self._velocity = pygame.math.Vector2(particle_type._velocity_fn())
        self._offset = particle_type._offset_fn()
        self._colour_fn = particle_type._colour_fn
        self.set_position(position)
        self._state = PARTICLE_ALIVE

    def set_position(self, position: pygame.math.Vector2):
        self._position = position + self._offset

    def _update_lifetime(self, dt_sec: float) -> None:
        if self._state == PARTICLE_DEAD:
            return
        self._lifetime_current -= dt_sec
        self._lifetime_ratio = 1 - (self._lifetime_current / self._lifetime_total)
        if self._lifetime_ratio >= 1:
            self._state = PARTICLE_DEAD
            return

    def update(self, dt_sec: float) -> None:
        self._update_lifetime(dt_sec)
        if self._state == PARTICLE_DEAD:
            return
        delta = pygame.math.Vector2(
            self._velocity.x * dt_sec, self._velocity.y * dt_sec
        )
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
        self.update_position(position)
        self._particle_weighting: int = self._calc_weighting(particle_types)
        self._particle_types = particle_types
        self._particles: List[Particle] = self._create_particles(nparticles)
        self._perpetual = perpetual

    def update_position(self, position: pygame.math.Vector2):
        self._position = position

    def _calc_weighting(self, particle_types: List[ParticleType]) -> int:
        weighting_total: int = 0
        for particle_type in particle_types:
            weighting_total += particle_type._weighting
        return weighting_total

    def _create_particle(self):
        particle_type = self._get_particle_type()
        particle = Particle(particle_type, self._position)
        return particle

    def _create_particles(self, nparticles: int) -> List[Particle]:
        particles = []
        for _ in range(nparticles):
            particle = self._create_particle()
            particles.append(particle)
        return particles

    def _get_particle_type(self) -> ParticleType:
        random_value: int = randint(0, self._particle_weighting)
        return self._find_particle_type(random_value)

    def _find_particle_type(self, value: int):
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
        if self._state == EMITTER_RUNNING:
            self.update(0)

    def update(self, dt_sec: float) -> None:
        if self._state != EMITTER_RUNNING:
            return
        [particle.update(dt_sec) for particle in self._particles]

        for particle in self._particles:
            if particle._state == PARTICLE_DEAD and self._perpetual:
                random_value = randint(0, self._particle_weighting)
                particle_type = self._find_particle_type(random_value)
                particle.create_from_type(particle_type, self._position)
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
                    screen,
                    particle.colour(),
                    (int(particle._position.x), int(particle._position.y), size, size),
                )
