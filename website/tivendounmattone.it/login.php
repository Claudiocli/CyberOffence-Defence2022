<?php
     $cn = pg_connect("host=localhost port=5432 user=postgres password=root");

    if($cn) {
        $query = pg_prepare($cn, "my_query", "SELECT * FROM users WHERE username = $1 and passwd = $2");
        $result = pg_execute($cn, "my_query", array($_POST['uname'], $_POST['psw']));

        $resul_num_rows = pg_num_rows($result);
        
        if($resul_num_rows > 0) { // If there are rows in the response, than do the redirect
            $username = pg_fetch_result($result, 0, 0); //result, row of result (just a row in our case), column to print
            $account_type = pg_fetch_result($result, 0, 2);
            
            setcookie('username', $username, $httponly = false);
            setcookie('account_type', $account_type, $httponly = false);
            header('Location: dashboard.php');
        }else{
            // header('Location: index.html');
            // echo '<h1 style="color:red">invalid username or password</h1>';
            $dom = new DOMDocument();
            $dom->loadHTMLfile("index.html");
            
            $username_form = $dom->getElementById('username');
            $pwd_form = $dom->getElementById('password');
            $text = $dom->getElementById('invalid-text');
            
            $username_form->setAttribute('class', 'wrong');
            $pwd_form->setAttribute('class', 'wrong'); 
            $text->setAttribute('class', 'wrong');

            print $dom->saveHTML();
        }
    }

    pg_close($cn);
?>