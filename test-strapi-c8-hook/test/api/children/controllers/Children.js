'use strict';

/**
 * Children.js controller
 *
 * @description: A set of functions called "actions" for managing `Children`.
 */

module.exports = {

  /**
   * Retrieve children records.
   *
   * @return {Object|Array}
   */

  find: async (ctx) => {
    if (ctx.query._q) {
      return strapi.services.children.search(ctx.query);
    } else {
      return strapi.services.children.fetchAll(ctx.query);
    }
  },

  /**
   * Retrieve a children record.
   *
   * @return {Object}
   */

  findOne: async (ctx) => {
    if (!ctx.params._id.match(/^[0-9a-fA-F]{24}$/)) {
      return ctx.notFound();
    }

    return strapi.services.children.fetch(ctx.params);
  },

  /**
   * Count children records.
   *
   * @return {Number}
   */

  count: async (ctx) => {
    return strapi.services.children.count(ctx.query);
  },

  /**
   * Create a/an children record.
   *
   * @return {Object}
   */

  create: async (ctx) => {
    return strapi.services.children.add(ctx.request.body);
  },

  /**
   * Update a/an children record.
   *
   * @return {Object}
   */

  update: async (ctx, next) => {
    return strapi.services.children.edit(ctx.params, ctx.request.body) ;
  },

  /**
   * Destroy a/an children record.
   *
   * @return {Object}
   */

  destroy: async (ctx, next) => {
    return strapi.services.children.remove(ctx.params);
  }
};
