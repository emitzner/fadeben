<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <meta name="description" content="">
        <meta name="author" content="">
        <link rel="shortcut icon" href="../../assets/ico/favicon.png">

        <title>Signin Template for Bootstrap</title>

        <!-- Bootstrap core CSS -->
        <link href="/css/bootstrap.min.css" rel="stylesheet">

        <!-- Custom styles for this template -->
        <link href="signin.css" rel="stylesheet">

        <!-- HTML5 shim and Respond.js IE8 support of HTML5 elements and media queries -->
        <!--[if lt IE 9]>
            <script src="../../assets/js/html5shiv.js"></script>
            <script src="../../assets/js/respond.min.js"></script>
            <![endif]-->
    </head>

    <body>

        <!-- Static navbar -->
        <div class="navbar navbar-default navbar-static-top">
            <div class="container">
                <div class="navbar-header">
                    <button type="button" class="navbar-toggle" data-toggle="collapse" data-target=".navbar-collapse">
                        <span class="icon-bar"></span>
                        <span class="icon-bar"></span>
                        <span class="icon-bar"></span>
                    </button>
                    <a class="navbar-brand" href="#">FadeBen</a>
                </div>
                <div class="navbar-collapse collapse">
                    <ul class="nav navbar-nav navbar-right">
                        <li><a href="../navbar/">Home</a></li>
                        <li class="active"><a href="./">Standings</a></li>
                        <li><a href="../navbar-fixed-top/">Account</a></li>
                    </ul>
                </div><!--/.nav-collapse -->
            </div>
        </div>

        <div class="container">
            ${ next.body() }
        </div> <!-- /container -->

        <!-- Bootstrap core JavaScript
             ================================================== -->
        <!-- Placed at the end of the document so the pages load faster -->
        <!-- jQuery (necessary for Bootstrap's JavaScript plugins) -->
        <script src="//code.jquery.com/jquery.js"></script>
        <!-- Include all compiled plugins (below), or include individual files as needed -->
        <script src="/js/bootstrap.min.js"></script>
    </body>
</html>
