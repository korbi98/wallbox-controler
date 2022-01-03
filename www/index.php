<!doctype html>

<html>

<head>
    <title>Wallbox Controller</title>
</head>

<body style="text-align:center">

    <h1>Wallbox-Controller</h1>
    <h4>Latest status:</h4>


    <?php
        function exec_switch_command($cmd) {
            $command_exec = escapeshellcmd('/home/pi/wallbox_controller/wallbox_control.py '.$cmd);
            $str_output = shell_exec($command_exec);
            echo $str_output;
        }

        if(array_key_exists('enable_auto_button', $_POST)) {
            exec_switch_command("enable_auto");
        }
        else if(array_key_exists('activate_button', $_POST)) {
            exec_switch_command("activate");
        }
        else if(array_key_exists('deactivate_button', $_POST)) {
            exec_switch_command("deactivate");
        }

        exec_switch_command("status");
    ?>

    <div style="width: 100%; padding:24px; margin-top:16px">
    <form method="post">
        <input type="submit" name="enable_auto_button"
                class="button" value="Enable Auto" />

        <input type="submit" name="activate_button"
                class="button" value="Activate" />

        <input type="submit" name="deactivate_button"
                class="button" value="Deactivate" />

        <input type="submit" name="refresh_button"
                class="button" value="Refresh" />
    </form>
    </div>

    <img src="soc_over_time.png">
    <h4>Event Log:</h4>

    <?php
        $file = escapeshellarg("/home/pi/wallbox_controller/logs/event.log");
        echo nl2br( `tail -n 8 $file` );
    ?>
</body>
</html>

