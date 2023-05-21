from sqlalchemy import create_engine, text

engine = create_engine("YUR_PLANET_SCALE_PASSWORD",
                       connect_args={"ssl": {
                        # YOUR_CA_GIVEN_BY_PLANTE_SCALE
                        "ssl_ca": "/etc/ssl/cert.pem"
                        
                       }})