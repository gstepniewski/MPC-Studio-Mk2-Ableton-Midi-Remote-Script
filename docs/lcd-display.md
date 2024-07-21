---
layout: default
title: LCD Display
nav_order: 5
---

To get LCD to work
1. Go to the Remote Scripts directory in your User Library
2. Enter `MPC_Studio_Mk2`
3. Enter `lcd-control`
4. Run `npm install` (node must be installed!)
5. Run `node index.js` and keep it running while you're using Live


Most of the time, the display shows information about the currently selected navigation mode:
* TRACK name
  * SCENE number name (on scroll with shift)
* PARAMETER name (change by holding Sample Select and selecting a white pad)
  * PARAMETER value (on jog wheel turn)
* BROWSER (nothing else here for now, the APIs only allow building independent browser instances)

Dialogs appear for 3 seconds and inform about actions and changes:
  * Touch Strip mode (volume/pan/send a/send b)
  * Current tempo (also if changed from Live)
  * Parameter being changed using jog wheel
  * Octave in keyboard mode
  * Macro used (mode + pad)
  * Routing (in type, in channel, out type, out channel, monitor)
  * Device / Clip mode (shift + locate)

Better docs coming soon!