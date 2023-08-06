from google.cloud import storage

def publish_map(cartoframes_map : object, name : str) -> str:
    """
    Publishes a CartoFrames map by uploading it as an HTML blob to a cloud storage bucket and returns a publicly accessible URL.

    Args:
        cartoframes_map (object): The CartoFrames map object to be published.
        name (str): The name of the map.

    Returns:
        str: The URL of the published map.
    """
    name = name.replace(" ", "_")
    blob_name = f"maps/{name}"
    
    st_client = storage.Client()
    bucket = st_client.get_bucket("juanluisrto")
    blob = bucket.blob(blob_name)

    html = cartoframes_map._repr_html_()
    html = html.replace("height: 632px;", "height: 100%;") #makes maps full screen
    blob.upload_from_string(html, content_type="text/html")
    blob.cache_control = "no-cache"
    return f"http://maps.juanluis.me/{name}"