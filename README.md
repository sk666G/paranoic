# Paranoic

Paranoic is a Fabric client for Minecraft 1.21.11, built from the Open Zio codebase. It keeps the source project's broad module set and adds a distinct client identity, a clean build artifact, and data migration from existing Zio and Mio Fabric profiles.

## Features

- Combat, movement, player, render, HUD, world, and utility modules
- Click GUI, commands, keybinds, module profiles, friends, enemies, macros, and chat filters
- Optional Baritone, ViaFabricPlus, Xaero's Minimap, Sodium, Lithium, ImmediatelyFast, and Entity Culling integrations
- Bundled sounds, shaders, fonts, and resource overrides

Optional integrations are not required to launch the client. Their features remain unavailable when the corresponding mod is absent.

## Requirements

- Minecraft 1.21.11
- Fabric Loader 0.19.5 or newer and Fabric API
- Java 21 to run the client
- JDK 25 to run the Gradle build; Gradle compiles the mod with the Java 21 toolchain

## Build

```sh
./gradlew build
```

The remapped client jar is written to `build/libs/`. To launch the development client, run `./gradlew runClient`.

## Install

Copy the remapped `paranoic-*.jar` into the Fabric instance's `mods` directory alongside Fabric API. The first launch creates a `paranoic` data directory. If a `paranoic` directory is not already present, existing `zio` data is copied forward; older `mio-fabric` data is also supported.

## Source lineage

Paranoic is based on [Open Zio](https://github.com/minecraftlover74/open-zio), an optimized Java recreation of Mio 2.4.4. The inherited code retains its original notices and attribution. Paranoic is not affiliated with or endorsed by Mio.
