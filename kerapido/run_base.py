import base64
client_id = "CtGMNioCffSkkbm433mY14M46aMa"
client_secret = "EQzcttDdjBqt0IbmlTBvZf06Tlga"
encodedData = base64.b64encode(bytes(f"{client_id}:{client_secret}", "ISO-8859-1")).decode("ascii")
authorization_header_string = f"Authorization: Basic {encodedData}"
print(authorization_header_string)