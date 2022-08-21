import random

import pygame

from particle_system import ParticleEmitter, ParticleType


def lifetime_fn(range_min, range_max):
    return range_min + random.random() * (range_max - range_min)


def size_fn(lifetime_ratio):
    return 1 if lifetime_ratio > 0.5 else 2


def white_fn(lifetime_ratio):
    return (255, 255, 255)


def red_fn(lifetime_ratio):
    return (255, 0, 0)


def yellow_fn(lifetime_ratio):
    return (255, 255, 0)


def white_fade_fn(lifetime_ratio):
    return (255, 255, 255) if lifetime_ratio < 0.5 else (127, 127, 127)


def rand_speed_fn(speed):
    return speed * (0.1 + random.random() * 0.9)


def circular_vector_fn(speed):
    return pygame.math.Vector2(speed, 0).rotate(random.random() * 360)


def offset_vector_fn(x, y):
    return pygame.math.Vector2(x, y)


def origin_vector_fn():
    return pygame.math.Vector2(0, 0)


def plume_vector_fn(x):
    return pygame.math.Vector2(0, x * (random.random() * 0.5))


def plume_vector2_fn(x):
    return pygame.math.Vector2(
        4 * (-1 + random.random() * 2), x * (0.25 + random.random() * 0.25)
    )


# ==========  PARTICLE TYPES ===============================================

explosion_particle1 = ParticleType(
    lambda: lifetime_fn(0.4, 0.6),
    100,
    lambda x: (255, 0, 0),
    lambda x: 2,
    circular_vector_fn,
    origin_vector_fn,
    lambda: rand_speed_fn(100),
)

explosion_particle2 = ParticleType(
    lambda: lifetime_fn(0.2, 0.4),
    100,
    lambda x: (255, 255, 0),
    lambda x: 2,
    circular_vector_fn,
    origin_vector_fn,
    lambda: rand_speed_fn(40),
)

explosion_particle3 = ParticleType(
    lambda: lifetime_fn(0.6, 0.8),
    80,
    lambda x: (255, 255, 255),
    lambda x: 2,
    circular_vector_fn,
    origin_vector_fn,
    lambda: rand_speed_fn(2000),
)

explosion_particle4 = ParticleType(
    lambda: lifetime_fn(0.2, 0.4),
    20,
    lambda x: (255, 255, 255),
    lambda x: 6,
    circular_vector_fn,
    origin_vector_fn,
    lambda: rand_speed_fn(500),
)

explosion_particle5 = ParticleType(
    lambda: lifetime_fn(0.2, 0.4),
    5,
    lambda x: (255, 0, 0),
    lambda x: 6,
    circular_vector_fn,
    origin_vector_fn,
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
    plume_vector2_fn,
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
