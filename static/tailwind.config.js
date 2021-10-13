module.exports = {
  mode: "jit",
  purge: {
    content: ["../templates/**/*.html", ],
    options: {
      safelist: ["bg-green-400", "bg-yellow-400", "bg-red-400"],
    },
  },
  darkMode: false, // or 'media' or 'class'
  theme: {
    extend: {
      fontFamily: {
        sans: ["Montserrat", "Helvetica", "Arial", "sans-serif"],
      },
    },
  },
  variants: {
    extend: {},
  },
  plugins: [],
};
