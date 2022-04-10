<!doctype html>

<html>

<head>
    <title>Wallbox Controller</title>
</head>

<style>
    table {margin-left:auto;margin-right:auto; text-align:left}
    td, th {padding-left: 10px; padding-right: 10px;}
    html {margin:    0 auto; max-width: 100vh; }
    img { display: block; margin: 0 auto }
    body { text-align:center; background-color: #F8EEA6; color: black; max-width: 100%; }
    .button {
        background-color: #225A8A;
        color: white;
        border: none;
        transition-duration: 0.4s;
        padding: 12px 16px;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        border-radius: 5px;
        font-size: 18px;
        box-shadow: 0 6px 8px 0 rgba(0,0,0,0.24), 0 17px 50px 0 rgba(0,0,0,0.19);
    }
    .button:hover {
        cursor: pointer;
        background-color: #D5A84E; /* Green */
        color: black;
        box-shadow: 0 12px 16px 0 rgba(0,0,0,0.24), 0 17px 50px 0 rgba(0,0,0,0.19);
    }
</style>

<body>

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

    <div style="margin-top: 24px">
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
    <img src="soc_over_time_week.png">
    <br>
    <br>
    <a href="log.php"><h4>Event Log:</h4></a>
    <table>
        <tr>
            <th>Date&Time</th>
            <th>Event</th>
            <th>Comment</th>
        </tr>
        <?php
            $file = file("/home/pi/wallbox_controller/logs/event.log");
            
            $index = 0;
            foreach(array_reverse($file) as $line)
            {
                if ($index < 10) {
                    $row = str_getcsv($line);
                    echo "<tr>";
                    foreach($row as $col)
                    {
                        echo "<td>" . htmlspecialchars($col) . "</td>";
                    }
                    echo "</tr> \n";
                } 
                $index++;
            }
        ?>
    </table>
</body>
</html>

