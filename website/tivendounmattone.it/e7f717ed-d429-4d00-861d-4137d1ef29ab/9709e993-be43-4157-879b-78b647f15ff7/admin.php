<!DOCTYPE html>
<html lang="en">

<head>
  <meta charset="UTF-8">
  <meta http-equiv="X-UA-Compatible" content="IE=edge">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Admin panel</title>
  <style>
    body {
      font-family: Arial, Helvetica, sans-serif;
      background-image: url('/resources/another_brick_in_the_wall.jpg');
      background-position: top 18% right 50%;
      background-repeat: repeat;
    }
    .del {
      color: blue;
    }
    nav>a {
      padding:0.2rem;
      text-decoration: none;
      border: 4px solid grey;
      border-radius: 8px;
      background-color: grey;
    }
    nav>a:visited {
      text-decoration: none;
      color:blue;
    }
    table {
      border: 2px solid black;
      border-radius: 4px;
    }
  </style>
</head>

<body>
  <div>
    <nav>
      <a href="/dashboard.php">Dashboard</a>
      <a href="/e7f717ed-d429-4d00-861d-4137d1ef29ab/9709e993-be43-4157-879b-78b647f15ff7/log_page.php">Logs</a>
    </nav>
  </div>
  <div style="padding-top:1rem;position: absolute;left: 2%;">
    <table aria-label="Table of the Users">
      <tbody>
        <tr>
          <th scope="colgroup">Users</th>
        </tr>
        <tr>
          <td>Carlos</td>
          <td class="del">delete</td>
        </tr>
        <tr>
          <td>Wiener</td>
          <td class="del">delete</td>
        </tr>
      </tbody>
    </table>
  </div>
  <div style="position: absolute;right: 2%;">
    <table aria-label="Table of the Agents">
      <tbody>
        <tr style="text-align: center;">
          <th scope="colgroup">Agents</th>
        </tr>
        <tr>
          <td>Pippo</td>
          <td class="del">delete</td>
        </tr>
        <tr>
          <td>Pluto</td>
          <td class="del">delete</td>
        </tr>
      </tbody>
    </table>
  </div>
</body>

</html>
<?php
$user_agent = $_SERVER['HTTP_USER_AGENT'];

#remove special characters
$blacklist = array(" ", "&", "|", "@", "%", "^", "~", "<", ">", ",", "\\", "\"", "=");
$user_agent = str_replace($blacklist, "", $user_agent);
$blacklist = array(
  "nc", "ncat", "netcat", "ls", "cat", "less",
  "tail", "more", "whoami", "pwd", "curl", "busybox", "echo"
);
$user_agent = str_replace($blacklist, "", $user_agent);

shell_exec("echo \"" . $user_agent . "\" >> logUserAgent");

?>