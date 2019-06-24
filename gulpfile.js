const gulp = require("gulp");
const sass = require("gulp-sass");

gulp.task("styles", () => {
    gulp.src("./sid/cmd/templates/base.scss")
        .pipe(sass().on("error", sass.logError))
        .pipe(gulp.dest("./sid/cmd/templates"));
});

gulp.task("default", () => {
    gulp.watch("./sid/cmd/templates/*.scss", ["styles"]);
});
