mkdir -p ~/.streamlit/
echo "\
[general]\n\
email = \"spencerwang2008@outlook.com\"\n\
" > ~/.streamlit/credentials.toml
echo "\
[server]\n\
headless = true\n\
enableCORS=false\n\
port = $PORT\n\
[theme]\n\
base=\"light\"\n\
primaryColor=\"white\"\n\
" > ~/.streamlit/config.toml
