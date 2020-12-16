# canitellmybosstofuckoff.com

This is a website for determining if you have enough money to tell your boss to
just fuck right off, and survive retirement ("fuck you money").

# DISCLAIMER

I am *NOT* a professional financial advisor or investor or expert or anything.
I just tell computers what to do for a living and one day I thought it'd be
cute and funny to tell them to do this in a single snarky page you can laugh at
and share with your friends.  This tool should encourage you to think about the
many benefits of not dying destitute, and seek professional help to ensure you
do not.  _*Use the calculations provided herein for anything beyond your own
entertainment only at your own financial peril!*_

Also, in case anyone is wondering, I actually like my boss and my job a lot
right now.  IT'S JUST A FIGURE OF SPEECH, OK? =D

# WHY DID I MAKE THIS?

Why not?

# DEVELOPMENT

Recommend pyenv, python 3.9.0.

    $ pyenv install 3.9.0
    $ pyenv virtualenv cani
    $ pyenv local cani
    $ pip install -r requirements.txt
    $ bin/test.sh

You now have a local server running for testing!

# References

I consulted the following docs / tutorials while producing this site:

* https://www.digitalocean.com/community/tutorials/how-to-make-a-web-application-using-flask-in-python-3
* https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-gunicorn-and-nginx-on-ubuntu-18-04
* https://getbootstrap.com/docs/5.0/getting-started/download/
* https://stackoverflow.com/questions/9786102/how-do-i-parallelize-a-simple-python-loop
* https://stackoverflow.com/questions/1427255/is-there-a-python-caching-library

# Dependencies and Thanks

This project would have been impossible, or much more difficult, were it not for:
* Python
* Flask
* Jinja
* Gunicorn
* Nginx
* Git

The site is hosted on my colo which runs cmyers.org and uses Joker.com for DNS.

# TODO

These are just my notes about features I might implement

## Short Term
* The cache is not shared between gunicorn workers.  Whoops.  Should probably fix that.
* Help text on each field explaining it in greater detail
* perma-link to a set of parameters

## Medium-Term
* Better SEO / discoverability
* Nav bar elements don't show which page is active dynamically
* plot of average $ left each year?  see matplotlib in python?

## Long Term
* the whole thing is just fugly.  Needs TLC.
* More careful consideration of taxes in the calculation.  For example,
  distributions are pre-tax but social security is post-tax (I think?)
* I should probably have a plan for what to do if this blows up and/or gets
  DOS'd.  This will definitely be the most CPU intensive thing on my colo'd
  server if it gets any traffic at all.
