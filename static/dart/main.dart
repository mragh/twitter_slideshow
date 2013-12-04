import 'dart:html';
import 'dart:convert' show JSON;
import 'dart:async' show Future;

DivElement photoElement;
SpanElement userNameElement;
SpanElement screenNameElement;
ParagraphElement textElement;

void main() {
    photoElement = querySelector("#tweet-photo");
    userNameElement = querySelector("span.user_name");
    screenNameElement = querySelector("span.screen_name");
    textElement = querySelector(".status p");
    photoElement.onClick.listen(randomPhoto);
}

void randomPhoto(Event e) {
    getRandomStatus().then(updateCurrentStatus);
}

void updateCurrentStatus(String jsonString){
    Map status = JSON.decode(jsonString);
    userNameElement.text = status['status']['user']['name'];
    screenNameElement.text = status['status']['user']['screen_name'];
    textElement.text = status['status']['text'];
    photoElement.style
                    ..width = "${status['image']['width']}px"
                    ..height = "${status['image']['height']}px"
                    ..background = "#3E3E50 url(${status['image']['url']})";
}

Future getRandomStatus() {
    var path = '/status/random';
    return HttpRequest.getString(path);
  }