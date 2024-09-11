# src

## File structure

- `database/` contains database scripts
- `rosbag-uploader` contains the Python webserver for uploading rosbags

## Deployement

⚠️ **Start out by replacing all the placeholder passwords** ⚠️
In particular all cases of `CHANGE_ME` and `Replace_me_wh3n_deploying_on_public_server` should be updated with the values from the ARIS wiki.

Make sure docker compose is installed. See https://docs.docker.com/engine/install/ubuntu/

For initial setup first run the setup docker compose file first.

Optional: Update URL in `Caddyfile` in case the domain changed.

Optional: Update `docker-compose.setup.yml` to point to the SQL file containing an existing database dump.

```sh
docker compose -f docker-compose.setup.yml up
```

Wait for it to finish, then exit the database (`CTRL`+`C`) and remove the created containers again.
```sh
docker compose -f docker-compose.setup.yml down
```

After that and for continuous deployment, run docker compose file in this directory.

You can run it in attached mode once for checking that everything works.
```sh
docker compose up
```

For proper deployment, run it in detached mode:
```sh
docker compose up -d
```

After this you should be done

If you want to remove containers again:
```sh
docker compose down
```
