const mix = require("laravel-mix");

mix
  .styles("src/css/*.css", "dist/app.css")
  .js("src/app.js", "dist")
  .sourceMaps();
