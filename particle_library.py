from particle_system import ParticleEmitter, ParticleType
import pygame
import random

lifetime_fn = lambda x, y: x + random.random() * (y - x)
size_fn = lambda x: 1 if x > 0.5 else 2
white_fn = lambda x: (255, 255, 255)
white_fade_fn = lambda x: (255, 255, 255) if x < 0.5 else (127, 127, 127)
red_fn = lambda x: (255, 0, 0)
yellow_fn = lambda x: (255, 255, 0)
rand_speed_fn = lambda x: x * (0.1 + random.random() * 0.9)
offset_origin_fn = lambda: pygame.math.Vector2(0, 0)
vector_circular_unit_vector_fn = lambda x: pygame.math.Vector2(x, 0).rotate(
    random.random() * 360
)
vector_2_fn = lambda x: pygame.math.Vector2(100, 0)
offset_fn = lambda x, y: pygame.math.Vector2(x, y)

# ==========  PARTICLE TYPES ===============================================

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

explosion_types = [
    explosion_particle1,
    explosion_particle2,
    explosion_particle3,
    explosion_particle4,
    explosion_particle5,
]


class ParticleExplosion:
    def __init__(self, position: pygame.math.Vector2) -> None:
        self._emitter = ParticleEmitter(300, explosion_types, position)

    def turn_on(self):
        self._emitter.turn_on(True)

    def draw(self, screen):
        self._emitter.draw(screen)

    def update(self, dt_sec: float):
        self._emitter.update(dt_sec)


plume_vector_fn = lambda x: pygame.math.Vector2(0, x * (random.random() * 0.5))

plume_type1 = ParticleType(
    lambda: lifetime_fn(0.04, 0.2),
    2,
    yellow_fn,
    lambda x: 2,
    plume_vector_fn,
    lambda: pygame.math.Vector2(0, 0),
    lambda: 300,
)
plume_type2 = ParticleType(
    lambda: lifetime_fn(0.04, 0.2),
    2,
    red_fn,
    lambda x: 2,
    plume_vector_fn,
    lambda: pygame.math.Vector2(2, 0),
    lambda: 300,
)
plume_type3 = ParticleType(
    lambda: lifetime_fn(0.04, 0.2),
    5,
    red_fn,
    lambda x: 2,
    plume_vector_fn,
    lambda: pygame.math.Vector2(-2, 0),
    lambda: 300,
)
plume_type4 = ParticleType(
    lambda: lifetime_fn(1.5, 1.8),
    10,
    white_fn,
    lambda x: 1,
    plume_vector_fn,
    lambda: pygame.math.Vector2(0, 2),
    lambda: 120,
)

plume_types = [plume_type1, plume_type2, plume_type3, plume_type4]


class ParticleJetPlume:
    def __init__(self, position: pygame.math.Vector2) -> None:
        self._emitter = ParticleEmitter(50, plume_types, position, True)

    def update_position(self, position):
        self._emitter.update_position(position)

    def turn_on(self):
        self._emitter.turn_on(True)

    def draw(self, screen):
        self._emitter.draw(screen)

    def update(self, dt_sec: float):
        self._emitter.update(dt_sec)
