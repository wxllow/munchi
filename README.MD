# Munchi

***Munchi is early in development, expect major changes that may break cogs or other functionality***

![GitHub forks](https://img.shields.io/github/forks/wxllow/munchi) ![GitHub stars](https://img.shields.io/github/stars/wxllow/munchi) ![GitHub contributors](https://img.shields.io/github/contributors/wxllow/munchi) ![License](https://img.shields.io/github/license/wxllow/munchi)

An open-source, multi-functional Discord bot written in Python, using slash commands!

## Goals

- Be easily extendable by others with cogs
- Have all the main functionality servers need, without the bloat
- Simple dashboard for configuring and changing settings
- Easy to use, host, and develop for

## Invite

You can invite Munchi to your server using the following link

<https://discord.com/api/oauth2/authorize?client_id=967137754024669284&permissions=8&scope=bot%20applications.commands>

## Dashboard

Coming soon...

## Project Layout

`/docs` - Documentation

`/cogs` - Cogs for the bot (this is where commands and other stuff are)

`/munchi` - The core bot

`/dashboard` - The Munchi dashboard

`/dashboard/backend` - The backend for the dashboard

`/dashboard/client` - The frontend for the dashboard

`/res` - Resources for the bot

## Hosting/Development Guide

### Installing dependencies

Munchi uses Poetry for installing/managing dependencies.

```bash
poetry install
```

### Configuring

To configure the bot, create a config.toml file in the directory of the bot. See resources/config.toml for an example.

### Running

Once you have configured the bot, you can now run it!

```bash
poetry run python main.py
```

### Dashbord

The dashboard has two parts, the backend and frontend, which must both be open and accessible on the web

#### Backend

Run the backend and make sure you open the port for it

```bash
poetry run python backend.py
```

#### Frontend

We recommend using a service like Vercel to host the dashboard. Make sure you modify the config at `dashboard/client/src/lib/config.ts` to reflect your bot.

### FAQ

> Why are some commands not responding but not giving any errors?

A common reason for this is that your database is not running. Make sure you have the correct database URL and that the database is running.
