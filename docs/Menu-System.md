# Menu system

This page explains how the menu system works

## Background
Originally this script was written in bash. After a while it became obvious that bash wasn't well suited to dealing with all the different types of configuration files, and logic that goes with configuring everything. IOTstack needs to be accessible to all levels of programmers and tinkerers, not just ones experience with Linux and bash. For this reason it was rewritten in Python, since the language syntax is easier to understand, and is more commonly used for scripting and programming that bash. Bash is still used in the project where it makes sense to use it, but the menu system itself uses Python.

## Menu Structure

Each screen of the menu is its own Python script. You can find most of these in the `./scripts` directory. When you select an item from the menu, and it changes screens, it actually dynamically loads and executes that Python script. It passes data as required by placing it into the global variable space so that both the child and the parent script can access it.

### Optimisations

It was obvious early on that the menu system would be slow on lower end devices, such as the Raspberry Pi, especially if you were rending a 4k terminal screen from a desktop via SSH. To mitigate this issue, not all of the screen is redrawn when there is a change. A "Hotzone" as it's called in the code is usually rerendered when there's a chance (such as pressing up or down to change an item selection). Full screen redraws are expensive and are only used when required.

### Sub-Menus

From the main screen, you will see several sections leading to various submenus. Most of these menus work in the same way as the main menu. The only exception to this rule is the Build Stack menu, which is probably the most complex part of IOTstack.

## Build Stack