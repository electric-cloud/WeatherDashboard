Plugin: HudsonDashboard
Version: 1.0

Description
===========

This plugin demonstrates the ability to create a tab that looks like the Hudson homepage.

Adding the Dashboard to a New Tab
=================================

To create a new tab:
- Install the plugin:
  - ectool installPlugin HudsonDashboard-1.0.jar
  - ectool promotePlugin HudsonDashboard-1.0 --promoted true

- Create a view with the new tab. For example, I created an 'ec_ui/availableViews/releaseView' property with this xml snippet:

<?xml version="1.0" encoding="utf-8"?>
  <view>
    <base>Default</base>
    <tab>
       <label>Hudson</label>
       <position>3</position>
       <url>/commander/pages/HudsonDashboard-1.0/hudsondashboard</url>
    </tab>
  </view>
