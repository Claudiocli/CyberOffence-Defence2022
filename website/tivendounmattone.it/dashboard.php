<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link href=/css/labsEcommerce.css rel=stylesheet>
    <title>TiVendoUnMattone</title>
</head>

<body>
    <div id="academyLabHeader">
    </div>
    <div theme="ecommerce">
        <section class="maincontainer">
            <div class="container">
                <section class="ecoms-pageheader">
                    <img src="/resources/logo-dashboard.png" alt="logo">
                </section>
                <section id="products-list" class="container-list-tiles">
                    <div>
                        <img src="/resources/ps5.jpg" alt="playstation5">
                        <h3>PS5 Digital (no perdi tempo).</h3>
                        <img src="/resources/sadrating.png" alt="rating">
                        $ 550
                        <a class="button" href="">View details</a>
                    </div>
                    <div>
                        <img src="/resources/stockdips5.jpg" alt="stock di playstation5">
                        <h3>Stock di 200 PS5 nuove ancora imballate.</h3>
                        <img src="/resources/sadrating.png" alt="rating">
                        $ 110K
                        <a class="button" href="">View details</a>
                    </div>
                    <div>
                        <img src="/resources/iphone14.jpg" alt="Iphone 14">
                        <h3>iPhone14 Pro Max 1TB RAM 1PB ROM.</h3>
                        <img src="/resources/sadrating.png" alt="rating">
                        $ 1029
                        <a class="button" href="">View details</a>
                    </div>
                    <div>
                        <img src="/resources/iphone14rotto.jpg" alt="Iphone 13">
                        <h3>iPhone14 rotto - solo per pezzi di ricambio.</h3>
                        <img src="/resources/sadrating.png" alt="rating">
                        $ 300
                        <a class="button" href="">View details</a>
                    </div>
                    <?php
                    $cn = pg_connect("host=localhost port=5432 user=postgres password=root");

                    if ($cn) {
                        $query = pg_prepare($cn, "my_query", "SELECT account_type FROM users WHERE username = 'Admin'");
                        $result = pg_execute($cn, "my_query", array());
                        $account_type = pg_fetch_result($result, 0, 0);
                        if (isset($_COOKIE["account_type"])) {
                            // Here there is the type juggling `md5('RSnakeXKPLlGdf2gYf')` will yeld 054bfc7be96181cc7e3f6b7a10baf38f
                            if (md5($_COOKIE['account_type']) == md5($account_type)) {
                                echo '<div>';
                                include 'image.php';
                                echo '<h3 id="image.php?file=www/web/images/goldenwall4admin.jpg - try to catch the flag.txt ;)">A special golden wall just for admin ;) </h3><img src="resources/happyrating.png">$ FREE4U<a class="button" href="">View details</a></div>';
                            }
                        }
                    }
                    pg_close($cn);
                    ?>
                </section>
            </div>
        </section>
    </div>
    <footer>
        <img id="graphic_needed_image" src="/resources/graphic_needed.png" alt="We need a Graphic">
        <p style="color:white; margin:0 0 0 !important;">&copy; TiVendoUnMattoneSRL 2k22</p>
    </footer>
    <script>
        const b = Array.from(document.getElementsByClassName('button'));
        b.forEach(element => {
            if (Math.random() <= 0.5) {
                element.href = 'https://youtu.be/dQw4w9WgXcQ';
            } else {
                element.href = 'https://youtu.be/R9bKmv2S9CE';
            }
        });
        // const g = document.getElementById('graphic_needed_image');
    </script>
</body>

</html>