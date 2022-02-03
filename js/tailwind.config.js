module.exports = {
  future: {
    removeDeprecatedGapUtilities: true,
    purgeLayersByDefault: true,
  },
  purge: {
    enabled: true, //true for production build
    content: ["../**/templates/*.html", "../**/templates/**/*.html"],
  },
  theme: {
    extend: {
      spacing: {
        '128': '32rem',
      }
    }
  },
  variants: {},
  plugins: [],
};
