# Knowledge Structure

## Purpose

Define the organization and classification structure for reusable knowledge.

## Structure

Knowledge is organized using categories and subcategories structure:

`knowledge/<category>/<subcategory>/`

## Categories

`knowledge/devices/`
Hardware devices, development boards, sensors, actuators, and peripherals.

`knowledge/software/`
Applications, tools, frameworks, and software systems.

`knowledge/programming/`
Programming languages, libraries, APIs, and development techniques.

`knowledge/electronics/`
Electronic components, circuits, interfaces, and electrical concepts.

`knowledge/networking/`
Network technologies, protocols, and communication systems.

`knowledge/operating-systems/`
Operating systems, administration, configuration, and troubleshooting.

`knowledge/ai/`
Artificial intelligence, machine learning, LLMs, and AI tools.

## Subcategories

Subcategories are folders inside an existing category used to group related knowledge.

Use subcategories when needed for better organization.

Example:

`knowledge/devices/`
- `boards/` → Development boards (Arduino UNO, Arduino MEGA 2560, ESP32 DevKit, etc.)
- `microcontrollers/` → Bare microcontroller chips (ATmega328P, ATmega2560, ESP32, STM32, etc.)
- `sensors/` → Sensor modules (temperature, humidity, IMU, etc.)
- `actuators/` → Actuator modules (motors, relays, servos, etc.)

Create a subcategory only when multiple related knowledge files justify separate organization.

Subcategories should:
- remain inside their parent category.
- follow the purpose of the parent category.
- avoid overlapping classifications.

## File Placement

Knowledge files should be stored inside the category that best matches their primary subject.

Use the most specific existing category or subcategory available.

## Indexing

Indexes are generated from knowledge files.

Indexes help agents discover and navigate knowledge but do not replace the source files.
