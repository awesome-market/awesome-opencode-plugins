# microchooser

**Microcontroller chooser / MCU selector.** Tell it what you're connecting (UART, I²C, SPI, CAN, CAN-FD, USB, SD card, Ethernet, Wi-Fi, BLE, LoRa, ADC, PWM, GPIO…), how big it can be and whether you want a dev board or a bare chip. It picks the **cheapest, most convenient** microcontroller or dev board that does all of it, with **buy links** and **KiCad symbols + footprints**. It also picks the parts around it: buck converters, battery chargers, communication ICs, cameras, LiDAR and ToF sensors.

**[Open the web app → apr0t0.github.io/microchooser](https://apr0t0.github.io/microchooser/)** (free)

![Ask your agent, get parts you can order](images/01-agent.png)

## For AI agents

Agent access is the **microchooser skill**, a one-time purchase on agensi.io:

**[Get the microchooser skill on agensi.io →](https://www.agensi.io/skills/microchooser)**

- **Real numbers, not recall.** 149 MCU families, 453 orderable part numbers, 130 dev boards and 144 power, comms and sensor parts. Every spec comes from a datasheet, with LCSC numbers and indicative prices.
- **Ranks like an engineer.** Cheapest part that does everything, with penalties for what bites later: a programmer to flash it, QFN or BGA packages, no Arduino or MicroPython, extra helper chips. If a chip is one CAN-FD short, it prices in an MCP2518FD.
- **Picks the parts around it.** Buck converters, battery chargers, CAN-FD / RS-485 / EtherCAT transceivers, cameras and LiDAR / ToF. It re-checks the MCU has the UART, CAN controller or camera port each part needs, and links a sized application circuit for every buck converter.
- **KiCad files for every IC.** Official KiCad symbols and footprints where they exist. Everything else is generated to IPC-7351B from the package drawing, as one zip per part.
- **Grounded web search.** When you want live stock, a datasheet check or a part the catalog doesn't have, the agent searches distributors and datasheets and cites what it finds.

Agensi loads the skill into Claude, Claude Code, Cursor, Codex, Gemini CLI, GitHub Copilot, Windsurf, VS Code, Cline over MCP ([connect guides](https://www.agensi.io/mcp)). Nothing to install or download, and updates are included. More on the [agents page](https://apr0t0.github.io/microchooser/#/agents).

Things to ask:

- "Which microcontroller should I use for a robot with 4 CAN-FD buses, an SD card and USB?"
- "Cheapest dev board with Wi-Fi and BLE that runs MicroPython and fits in a 25 mm enclosure."
- "Buck converter from a 6S LiPo to 5 V at 3 A. Give me the KiCad footprint."
- "Isolated CAN-FD transceiver for 3.3 V logic."
- "Global-shutter camera for a Raspberry Pi 5."
- "Cheapest 2D LiDAR for SLAM, and an MCU with a spare UART for it."

## The web app

![Peripherals in, the right microcontroller out](images/02-chooser.png)

- 149 MCU families, 453 orderable part numbers and 130 dev boards, plus 144 power, comms and sensor parts.
- Ranked by effective cost: price plus a penalty for anything inconvenient (needs a programmer, QFN/BGA, no Arduino or MicroPython, extra helper chips). If a chip is one peripheral short, it prices in an add-on chip.
- Official KiCad symbols and footprints where they exist; everything else generated to IPC-7351B.
- The whole query lives in the URL, so searches are shareable: [`?target=chip&canFd=4&sdCard=1…`](https://apr0t0.github.io/microchooser/?target=chip&canFd=4&sdCard=1&devices=usb-hub,led:3)

![Specs, prices and buy links](images/03-detail.png)

![KiCad symbol and footprint](images/04-kicad.png)

![The parts around the MCU](images/05-components.png)

## Wrong spec or missing part?

[Open an issue](https://github.com/aPR0T0/microchooser/issues). Fixes reach the website and the skill together.

---

This repository only hosts the website (the `gh-pages` branch is published automatically). Prices are indicative qty-1 USD. Check generated footprints against the datasheet before ordering boards. KiCad library parts © KiCad contributors, CC-BY-SA 4.0.
