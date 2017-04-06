Run the following from the root of the repository to launch the "fishr" app in debug mode:

```bash
mkdir -p data/fish_pics && export FLASK_APP=fishr/fishr.py && flask run --host=0.0.0.0 --debugger --reload
```

OR

`./run.sh`

Access on browser at: http://localhost:5000/
FYI: the app is launched on the local subnet. So, you can access it from your phone on your local LAN if you lookup your computer's local IP, probably: "192.168.0.*"
On linux run: `/sbin/ifconfig -a`
