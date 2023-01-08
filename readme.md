# Arcadian

A very simple little dodgem game.

There's a folder called music in the root... put your own _.mp3_ or _.ogg_ files in here and __Arcadian__ will play them while you dodge those pesky asteroids.

## Deployment

I've used __cx-freeze__ to create folders for each platform (linux, windows and macos).  For some reason MacOs will look to the user's home folder for the music and hiscore files.

## Things to do

- [x] add a start screen
- [x] display time correctly
- [x] fix transparency on player's ship image
- [x] add high score feature
- [x] load and save high score
- [x] update speed as game progresses
- [x] add music
- [x] add graphics for asteroids
- [x] add collision detection - use sprites for this?
- [x] deal with player death and game over
- [x] add sound effects
- [x] add particle effects
  - when ship blows up
  - ship's engines
- [x] Particle system code needs large clean up
- [x] PlayList class needs error handling
- [x] The asteroid code could down with some tidying up and refactoring
- [x] Add support for a controller
- [x] handle issue when controller disconnects

## Ideas for Future Versions (but not this version)

☣️ Danger ☣️ Feature Creep

- Add more asteroids as time increases
- Add collectable items?  Fuel maybe?
- Add aliens in there to shoot at?
- Change from time to a score - allows for other things,  e.g.
  - aliens to shoot
  - collectibles
  - bonus for using turbo boost
- speech bubbles (*"Never tell me the odds!"*)
