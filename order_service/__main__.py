# type: ignore[attr-defined]
import os

import uvicorn


def main() -> None:
    from order_service.app import order_app  # pylint: disable=import-outside-toplevel
    app = order_app
    port = int(os.environ.get("PORT", 5555))
    uvicorn.run(app, host="0.0.0.0", port=port, log_level="error")


if __name__ == "__main__":
    main()
