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

# TODO

These are just my notes about features I might implement

* More careful consideration of taxes in the calculation.  For example,
  distributions are pre-tax but social security is post-tax (I think?)
* Nav bar elements don't show which page is active dynamically
* the whole thing is just fugly.  Needs TLC.
* I should probably have a plan for what to do if this blows up and/or gets
  DOS'd.  This will definitely be the most CPU intensive thing on my colo'd
  server if it gets any traffic at all.

