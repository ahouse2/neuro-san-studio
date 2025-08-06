import os

# Feature toggle configuration. Each feature can be enabled/disabled
# via environment variables:
#   FEATURE_THEORIES, FEATURE_BINDER, FEATURE_CHAT
# Defaults are enabled.
FEATURES = {
    "theories": os.getenv("FEATURE_THEORIES", "1") == "1",
    "binder": os.getenv("FEATURE_BINDER", "1") == "1",
    "chat": os.getenv("FEATURE_CHAT", "1") == "1",
}
