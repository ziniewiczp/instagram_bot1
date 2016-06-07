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
        <select id="category" name="category">
          <option value="" disabled selected required >Select category</option>
          <option value="buildings">buildings</option>
          <option value="food">food</option>
          <option value="nature">nature</option>
          <option value="people">people</option>
          <option value="technology">technology</option>
          <option value="objects">objects</option>
        </select>


        <select id="time" name="timestamp">
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
