# Streamlit Cloud Deployment Guide 🚀

Now that Project Icarus has a modern UI, you can deploy it to the web for easy access.

## 1. Push the New Branch to GitHub
Run these commands in your VS Code terminal to upload the UI changes:

```bash
git push -u origin feature/streamlit-ui
```

## 2. Connect to Streamlit Cloud
1.  Go to [Streamlit Cloud](https://share.streamlit.io/) and sign in with GitHub.
2.  Click **New app**.
3.  Select your repository: `MutentMan/Project-Icarus`.
4.  Set **Branch** to: `feature/streamlit-ui`.
5.  Set **Main file path** to: `app.py`.
6.  Click **Deploy!**

## 3. Configure Secrets (Optional)
If you want to bake your API keys into the app so you don't have to enter them every time:
1.  On your app dashboard in Streamlit Cloud, go to **Settings** -> **Secrets**.
2.  Add your keys in TOML format:
    ```toml
    [api_keys]
    haveibeenpwned = "YOUR_KEY_HERE"
    numverify = "YOUR_KEY_HERE"

    [ai_engine]
    enabled = true
    model = "llama3"
    # Note: Local AI (Ollama) won't work in the cloud unless you use a hosted LLM API.
    ```

Your app will be live at a custom `streamlit.app` URL!
