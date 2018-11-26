# Scraping Proxy Tor

Tutorial en Español: https://jarroba.com/scraping-anonimo-la-red-tor/

Tutorial in English: https://jarroba.com/anonymous-scraping-by-tor-network/

Python, Tor, Stem, Privoxy: with this tools, allow requests new connections via 
Tor for obtain new IP addresses.

## Scraping with Tor in Python

The most common use-case when you are scraping a website is to be able to change
 your identity (IP) using TOR (or a proxy that rotate an IP) when you have been 
 done multiple requests per unit time with the same IP in a website 
 (like google) and don't block your connection and you can continue scraping 
 this website.

## Configuration

For this program it's necessary install in a one Linux distribution (in this 
case the author has used Linux Mind) the next tools:

-**Tor**

-**Stem:** is a Python controller library for tor.

-**Privoxy:** is a non-caching web proxy with advanced filtering capabilities 
for enhancing privacy, modifying web page data and HTTP headers, controlling 
access, and removing ads and other obnoxious Internet junk. Privoxy has a 
flexible configuration and can be customized to suit individual needs and 
tastes. It has application for both stand-alone systems and multi-user networks.

### Tor

Install Tor.

```
sudo apt-get update
sudo apt-get install tor
sudo /etc/init.d/tor restart
```

*the socks listener is on port 9050.*

Next, do the following:

- Enable the ControlPort listener for Tor to listen on port 9051, as this is the
 port to which Tor will listen for any communication from applications talking 
 to the Tor controller.
- Hash a new password that prevents random access to the port by outside agents.
- Implement cookie authentication as well.

You can create a hashed password out of your password using:
	
```
tor --hash-password my_password
```

In this case i put **1234** proof password. The hash password generated is:

´´´
16:9529EB03A306DE6F60171DE514EA2FCD49235BAF1E1E55897209679683
´´´

Then, update the /etc/tor/torrc with the port, hashed password, and cookie authentication.

```
sudo vim /etc/tor/torrc
```

```
ControlPort 9051
# hashed password below is obtained via `tor --hash-password my_password`
HashedControlPassword 16:9529EB03A306DE6F60171DE514EA2FCD49235BAF1E1E55897209679683
CookieAuthentication 1
```

Restart Tor again to the configuration changes are applied.
	
```
sudo /etc/init.d/tor restart
```

if you have any problems, you can enable control port using --controlport flag 
as follows:

```
tor --controlport 9051 &
```


### python-stem

Install **python-stem** which is a Python-based module used to interact with the
Tor Controller, letting us send and receive commands to and from the Tor Control
 port programmatically.

```
sudo apt-get install python-stem

# for python3
sudo apt-get install python3-stem
```

### privoxy

Tor itself is not a http proxy. So in order to get access to the Tor Network, 
use **privoxy** as an http-proxy though socks5.

Install **privoxy** via the following command:
	
```
sudo apt-get install privoxy
```

Now, tell **privoxy** to use TOR by routing all traffic through the SOCKS 
servers at localhost port 9050.

```
sudo vim /etc/privoxy/config
```

and enable **forward-socks5** as follows:
	
```
forward-socks5 / 127.0.0.1:9050 .
```

Restart **privoxy** after making the change to the configuration file.
	
```
sudo /etc/init.d/privoxy restart
```
