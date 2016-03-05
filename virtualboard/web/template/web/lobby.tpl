{% extends 'web/base.tpl' %}
{% load staticfiles %}


{% block head %}
  <link rel="stylesheet" type="text/css" href="{% static 'lobby.css' %}">
  <link rel="stylesheet" href="{% static 'board/board.css' %}">

  <script type="text/javascript" src="{% static 'board/babylon.js' %}"></script>
  <script type="text/javascript" src="{% static 'board/vboard.js' %}"></script>

  <script type="text/javascript" src="{% static 'chat.js' %}"></script>
{% endblock %}

{% block content %}
  {% if not lobby_instance %}
    <h1>critical error: lobby instance not ready</h1>
    
  {% else %}
    <canvas id="canvas">
      If you can see this, your browser may not support HTML 5.
    </canvas>

    <!--
    <div class="container container-table">
      <div class="row vertical-center-row">
        <div class="text-center col-md-4 col-md-offset-4">
          <h1 id="welcome">Hi {{ user_id }}! Welcome to lobby #{{ lobby_instance.id }}『{{ lobby_instance.name }}』<h1>
          <p>{{ lobby_instance.num_members }} players</p>

          <button type="button" class="btn btn-primary">start game</button>
          <a href="{% url 'web:leavelobby' lobby_instance.id %}" class="btn btn-danger">leave</a>
        </div>
      </div>
    </div>


    <div id="chatbox">
      <div id="inbox">
      </div>
      <div id="input">
        <form action="message/new/" method="post" id="messageform">
          <table>
            <tr id="text-entry">
              <td><input name="body" id="message" style="width:500px"></td>
              <td style="padding-left:5px">
                <input type="submit" value="{{ _("Post") }}">
                <input type="hidden" name="user_id" value="{{ user_id }}">
                <input type="hidden" name="next" value="{{ request.path }}">
              </td>
            </tr>
          </table>
        </form>
      </div>
    </div>

    <script>
      var lobby_id = {{ lobby_instance.id }};
    </script>
    
    -->

  {% endif %}
{% endblock %}