# Pretix Email Template for NETWAYS

This is a plugin for Pretix that creates a custom template for emails.

It consists of 2 boxes in the main part and a footer with signature and logos. 
In the first box, after the event title, the first paragraph with the greeting is blue, the respective customer name can be dynamically set via the email settings under ``Email Content`` with the variable ``{name}`` or ``{name_for_salutation}``.

In the second box the order details are displayed

In the template you can optionally show an event logo in the upper left corner and the signature is selectable in the Pretix GUI.

The first two lines of the signature are in blue color.
To the right of the signature are 4 social media icons with hyperlinks. The URLs of the icons and hyperlinks are hardcoded in the footer and must be changed manually if desired.

To the right of the signature are four social media icons for Twitter, Youtube, Facebook and Instagram.

## Installation:

Install the plugin with ``pip install pretix-net-mail``.

Then reconfigure Pretix with the commands ``python -m pretix rebuild && python migrate``.

Then restart the server with ``systemctl restart pretix-web pretix-worker`` (depending on the installation)


