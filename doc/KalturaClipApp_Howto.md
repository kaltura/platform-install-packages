Integrating the Kaltura ClipApp
===================

Author: Carise Fernandez

The Kaltura ClipApp provides a simple timeline editor so you can clip and trim Kaltura entries. It consists of 2 parts:

 - a Flash object that interacts with the KDP (the clipper)
 - Javascript that handles the user's interactions and provides an extra layer of customization for enabling some sort of backend (e.g. PHP, Java) to talk to the Kaltura services when saving changes to the edited entry.

This howto will walk you through what the code is doing in the PHP. It can also be applied for other integrations (e.g. Java, which I did), which is why the steps are a little tedious.

Setup steps
-----------

1. uiConfIds

    I am using the default uiConfIds for both the KDP and clipper. I don't know if there is a need to configure a custom uiConfId for the clipper, and I think I ran into a few glitches when using my own uiConfId for the KDP. The original demo code also uses these uiConfIds.

    KDP uiConfId: ```5674282```

    Clipper uiConfId: ```5674302```

2. Retrieve the KalturaMediaEntry data. The code in init.php already sets up the session and retrieves the KalturaMediaEntry for you.

    Initialize the Kaltura session. As a reminder, DO NOT put your adminSecret in your Javascript!

3. Look in your config.php (or similar) and fill in the configuration variables like your partnerId, adminSecret, etc.

4. Frontend: Include jQuery (I have been able to use the clipper with jQuery 1.11.1), the included jQuery time stepper plugin, clipApp.js, and the clipApp CSS. Initialize your Javascript clipApp as such. (Your init.php should already take care of this step for you.)

  ```jsp
      <script>
        clipApp.init( {
            "config": "<?php echo htmlspecialchars($_GET['config']);?>",
            "host": "<?php echo $conf['host'];?>",
            "partner_id": "<?php echo $conf['partner_id'];?>",
            "entry": <?php echo json_encode($entry);?>,
            "ks": "<?php echo $ks;?>",
            "kdp_uiconf_id": <?php echo $conf['kdp_uiconf_id']; ?>,
            "kclip_uiconf_id": <?php echo $conf['clipper_uiconf_id']; ?>,
            "redirect_save": <?php echo ($conf['redirect_save']) ? 'true' : 'false'; ?>,
            "redirect_url": "<?php echo $conf['redirect_url']; ?>",
            "overwrite_entry": <?php echo ($conf['overwrite_entry']) ? 'true' : 'false'; ?>
        });
      </script>```

5. Backend

    Configure your clipApp.js to point to your backend API. By default, it is hardcoded to save.php.

Conclusion
----------

If you have any questions, please feel free to ask questions on the Kaltura community forum.


References
----------
* [Kaltura ClipApp Live Demo](http://showcase.kaltura.com/demos/clipapp/index.php?cb=1410466358).
* [ClipApp ActionScript Code](https://github.com/kaltura/clipper).
* [ClipApp Javascript/PHP Code](https://github.com/kaltura/clipapp).
