// save object data from browser console to file
// -- credit to user 'ollieglass' for their post on CoderWall
// -- https://coderwall.com/p/prhwzg/add-console-save-to-chrome
console.save = (data, filename) => {
    if (!data) {
        console.error('Console.save: No data')
        return;
    }

    if (!filename) filename = 'story.json'

    if (typeof data === "object") {
        data = JSON.stringify(data, undefined, 4);
    }


    var blob = new Blob([data], {
            type: 'text/json'
        }),
        e = document.createEvent('MouseEvents'),
        a = document.createElement('a')

    a.download = filename
    a.href = window.URL.createObjectURL(blob)
    a.dataset.downloadurl = ['text/json', a.download, a.href].join(':')
    e.initMouseEvent('click', true, false, window, 0, 0, 0, 0, 0, false, false, false, false, 0, null)
    a.dispatchEvent(e)
}

save = () => {
  console.save(Array.from(all_emojis), 'emoji_names.json');
}

getCurrentEmojis = () => {
	current_emoji_rows = document.getElementsByClassName("ReactVirtualized__Grid__innerScrollContainer")[0].children
	all_emoji_names = Array.from(current_emoji_rows).map((row) => {
		emojis = Array.from(row.children)
		return emojis.map((emoji) => {
			return emoji.getAttribute("data-name")
		}).filter((emoji_name) => {
			return emoji_name !== null
        })
	})
	return [].concat.apply([], all_emoji_names)
}
emoji_picker = document.getElementById("emoji-picker-list")

scrollEmojiPicker = (n) => {
	emoji_picker.scroll(0, emoji_picker.scrollTop + n)
}

setEmojiPickerScroll = (n) => {
	emoji_picker.scroll(0, n)
}

all_emojis = new Set();
addCurrentEmojis = () => {
    current_emojis = getCurrentEmojis()
    current_emojis.map((current_emoji) => {
        all_emojis.add(current_emoji)
    })
}

navigate = () => {
    if (emoji_picker.scrollHeight - emoji_picker.scrollTop > 400) {
        scrollEmojiPicker(200)
        addCurrentEmojis()
    } else {
        save()
        stop()
    }
}

stepEvery = 1500
enabled = false

start = () => {
    enabled = true;
}

stop = () => {
    enabled = false;
}

let interval = undefined;
enableIntervalTrigger = () => {
    interval = setInterval(() => {
        if (enabled) {
            navigate();
        }
    }, stepEvery);
}

enableIntervalTrigger()

// modify the interval at which we trigger our code
const setSpeed = (n) => {
    clearInterval(interval);
    stepEvery = n;
    enableIntervalTrigger();
}

// enable our code trigger
setTimeout(enableIntervalTrigger, 1500);