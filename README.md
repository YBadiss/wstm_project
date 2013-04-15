wstm_project
============

Implementation of a music recommandation system.

Steps before running on a new machine:
	- Install SocksiPy (sudo apt-get install python-socksipy)
	- Install TorCtl (sudo apt-get install python-torctl)
	- Install TOR (sudo apt-get install tor)
	- Edit TOR's config file located in /etc/tor/torrc
		* Uncomment the line "ControlPort 9051"
	- Restart TOR (sudo /etc/init.d/tor restart)
