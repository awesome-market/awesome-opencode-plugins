**Prerequisites:**  Node.js

1. Install dependencies:
   `npm install`
3. Run the app:
   `npm run dev`

## Proactive Assistant Setup (Optional)

This app features a proactive assistant that offers context-aware suggestions. To enable it without an API key, you can run a self-hosted `llama.cpp` server.

1.  **Install llama.cpp:** Follow the [setup guide](https://github.com/ggerganov/llama.cpp).
2.  **Download Gemma:** Obtain the `Gemma-4-E2B-it-Assistant` GGUF model.
3.  **Start the server:**
    ```bash
    ./llama-server -m models/gemma-4-e2b-it.gguf --port 8080 --cors-allow-origin "*"
    ```
4.  The assistant in the web UI will automatically connect to `http://localhost:8080`.
