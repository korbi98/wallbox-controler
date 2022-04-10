<!doctype html>

<html>

<head>
    <title>Wallbox Log</title>
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
    <h2>Wallbox Controler Log</h2>
    <a href="index.php"><p style="margin-top: -8px">Go Back to Dashboard</p></a>
    <table style="margin-top: 16px">
    <tr>
    <th>Date&Time</th>
    <th>Event</th>
    <th>Comment</th>
    </tr>
<?php
$file = file("/home/pi/wallbox_controller/logs/event.log");

$index = 0;
$row_count = count($file);
foreach(array_reverse($file) as $line)
{
    // don't display last line as it is the header
    if ($index < 1000 && $index < $row_count-1) {
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