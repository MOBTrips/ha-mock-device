# Developer Notes

Mock Device is data-driven. Add devices in `models.py` and generated values in `store.py`.

Guidelines:

- Keep released entity keys stable.
- Prefer adding entities over renaming/removing entities.
- Keep generated data deterministic.
- Keep normal sensors read-only.
- Put user controls only on `Mock QA Console`.
- Preserve clean unload behavior in `async_unload_entry`.
- Do not create Home Assistant helpers, automations, dashboards, or external storage.

The generator persists only its own compact state through Home Assistant `Store`. This is intentional so restart behavior can be tested without creating external side effects.
