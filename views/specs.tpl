<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <link rel="stylesheet" type="text/css" href="static/main.css">
    <link rel="stylesheet" type="text/css" href="static/materialize.css">
    <title>InstaBot</title>
</head>
<body>
% include('navbar.tpl')

<div class="row">
    <div class="col s12">
      <div class="input-field col s12">
        <form action="/specs" method="post" enctype="multipart/form-data">
        <select id="category" name="category" required>
          <option value="" disabled selected required >Select category</option>
          <option value="Swimming">Swimming</option>
          <option value="Running">Running</option>
          <option value="Cars">Cars</option>
          <option value="Sports">Sports</option>
          <option value="Winter">Winter</option>
          <option value="Summer">Summer</option>
          <option value="Friends">Friends</option>
          <option value="Boys">Boys</option>
          <option value="Baby">Baby</option>
          <option value="People">People</option>
          <option value="Sea">Sea</option>
          <option value="Flower">Flower</option>
          <option value="Urban">Urban</option>
          <option value="Love">Love</option>
          <option value="Naure">Naure</option>
          <option value="Food">Food</option>
        </select>


        <select id="time" name="timestamp" required>
          <option value="" disabled selected required >Select timestamp</option>
          <option value="1">1hour</option>
          <option value="2">2hours</option>
          <option value="3">3hours</option>
          <option value="6">6hours</option>
          <option value="12">12hours</option>
          <option value="24">24hours</option>
        </select>
        <button class="btn btn-large waves-effect waves-light" id="loginButton" type="submit" >Submit</button>
      </form>
      </div>
    </div>
</div>

</div>
<script src="../static/jquery-1.12.3.min.js"></script>
<script src="../static/materialize.js"></script>
<script src="../static/main.js"></script>
</body>
</html>
