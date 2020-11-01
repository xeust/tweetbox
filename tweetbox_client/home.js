/** input in html file by Jinja template
 * 
import { h, app } from "https://unpkg.com/hyperapp@2.0.4/src/index.js";
let input = {{ note_data|tojson }};

*/




// effects


const attachTweets = async (dispatch, options) => {
    requestAnimationFrame(() => {
        const tweetMap = options.state.tweets;
        for (const tweet of Object.keys(tweetMap)) {
            const container = document.getElementById(tweet);
            container.innerHTML = tweetMap[tweet];
        }
    });
};



// views
const main = props => {
  return h("div", {class: "wrapper"}, [
      Object.keys(props.tweets).map(each => 
            h("div", {class: "tweet-wrapper", id: each}, [
            ])
      )
  ]);
};


/*
tweet:
{
    [ID]: html,
}
*/


const initState = {
    tweets: input
};

app({
    init: [initState,
        [
            attachTweets,
            { 
                state: initState, 
            }
        ]
    ],
    view: state => main(state),
    node: document.getElementById("app")
});