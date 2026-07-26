---
name: knowledge-subcategory-classifier
description: Classify vault subcategory; ask user when ambiguous.
category: knowledge-management
tags:
  - knowledge-base
  - classification
  - subcategory
---

# knowledge-subcategory-classifier

## Purpose

Provides explicit decision rules and agent behavior for assigning subcategories within the knowledge vault. Prevents misclassification by requiring user confirmation when ambiguous.

## Devices Category Subcategories

| Subcategory | Description | Examples |
|-------------|-------------|----------|
| `boards/` | Complete development boards with USB, power regulation, headers | Arduino UNO, Arduino MEGA 2560, ESP32 DevKit, Raspberry Pi, STM32 Nucleo |
| `microcontrollers/` | Bare microcontroller chips (MCUs) — no board components | ATmega328P, ATmega2560, ESP32 (chip), STM32F407, RP2040 |
| `sensors/` | Sensor modules and breakout boards | BME280, MPU6050, DHT22, VL53L0X, HC-SR04 |
| `actuators/` | Actuator modules and drivers | Stepper drivers (A4988, TMC2209), relay modules, servo controllers, motor drivers |

## Decision Rules

1. **If the subject has USB connector + power regulation + pin headers → `boards/`**
2. **If the subject is a bare chip (QFP, BGA, DIP package) → `microcontrollers/`**
3. **If the subject measures something → `sensors/`**
4. **If the subject moves/controls something → `actuators/`**

## Agent Behavior (MANDATORY)

**When subcategory is NOT explicitly specified in the task:**
- Agent MUST ask the user: "Should this go in `boards/`, `microcontrollers/`, `sensors/`, or `actuators/`?"
- Do NOT infer from filename, title, or content alone
- Example: "Arduino UNO" could be the board OR the MCU family — clarify

**When subcategory IS explicitly specified:**
- Use the specified subcategory
- Validate it exists in `knowledge_structure.md`

## Related Links Policy for `devices/`

- **Board pages**: link to their MCU (`related: ["ATmega328P"]`), optionally peer boards (`["Arduino MEGA 2560"]`)
- **MCU pages**: link to their primary board (`related: ["Arduino UNO"]`), sibling MCUs (`["ATmega2560"]`)
- **Do NOT** link boards to other boards as "alternatives" unless explicitly requested
- **Do NOT** add generic "see also" links to popular boards (ESP32, etc.) without user direction

## Template Variables

The `entity-page.md` template (in `knowledge-wiki` skill) uses:
- `subcategory: "{{subcategory}}"` — must be filled with `boards`, `microcontrollers`, `sensors`, or `actuators`
- `tags: []` — include the subcategory as a tag (e.g., `board`, `microcontroller`)
- `type: entity` — remains `entity` for all device subcategories

## Integration with knowledge-wiki Skill

This classifier is called during `knowledge_workflow.md` Step 2 (Classify) before page creation. The `knowledge-wiki` skill's `index_update()` validates the subcategory against known list.

## When to Extend

Add new subcategory rules here when:
- New category gets subcategories (e.g., `software/` → `libraries/`, `frameworks/`, `tools/`)
- New device types emerge that don't fit existing four
- User requests a new classification dimension