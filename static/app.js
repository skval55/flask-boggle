console.log("sup");

$("button").click(async function (e) {
  e.preventDefault();
  const wrd = $("input").val();
  console.log(wrd);
  await axios({
    method: "post",
    url: "http://127.0.0.1:5000/",
    data: {
      word: wrd,
    },
  });
});
