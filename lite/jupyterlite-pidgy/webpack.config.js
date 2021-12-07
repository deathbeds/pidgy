module.exports = {
  module: {
    rules: [
      {
        test: /pypi\/.*/,
        type: 'asset/resource'
      }
    ]
  }
};
