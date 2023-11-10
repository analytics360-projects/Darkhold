import jwt
import datetime
import uuid

token = jwt.encode(
	{
		"iss": "de530a92-8c2f-445f-ac55-26732063306b",
		"exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=5),
		"jti": str(uuid.uuid4()),
		"aud": "tableau",
		"sub": "Admin",
		"scp": ["tableau:views:embed", "tableau:metrics:embed" , "tableau:views:embed_authoring", "tableau:ask_data:embed"],
	},
		"ixp+Wmkh0gD1tc1+lw2q7cgBMkmpk6bDHMTp/TD+CFk=",
		algorithm = "HS256",
		headers = {
		'kid': "f25d6355-5167-478f-b053-8fb12ddbb33e",
		'iss': "de530a92-8c2f-445f-ac55-26732063306b"
        }
  )


print(token)