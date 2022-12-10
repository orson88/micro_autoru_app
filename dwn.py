import gdown

def get_pickle():
    url1 = "https://drive.google.com/uc?id=18zS71uxyIoYfH_xdVEhKxUClfIO3uAlB&export=download"
    output1 = "autoru_proj_data.pkl"
    gdown.download(url1, output1, quiet=False)

def get_csv():
    url2 = "https://drive.google.com/uc?id=1w0oqTnASkEpmh2EJKbvNubMQg9M0ssbo"
    output2 = "auto_data.csv"

    gdown.download(url2, output2, quiet = False)