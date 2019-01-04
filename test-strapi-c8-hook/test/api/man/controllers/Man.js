'use strict';

/**
 * Man.js controller
 *
 * @description: A set of functions called "actions" for managing `Man`.
 */

module.exports = {

  /**
   * Retrieve man records.
   *
   * @return {Object|Array}
   */

  find: async (ctx) => {
    if (ctx.query._q) {
      return strapi.services.man.search(ctx.query);
    } else {
      return strapi.services.man.fetchAll(ctx.query);
    }
  },

  /**
   * Retrieve a man record.
   *
   * @return {Object}
   */

  findOne: async (ctx) => {
    if (!ctx.params._id.match(/^[0-9a-fA-F]{24}$/)) {
      return ctx.notFound();
    }

    return strapi.services.man.fetch(ctx.params);
  },

  /**
   * Count man records.
   *
   * @return {Number}
   */

  count: async (ctx) => {
    return strapi.services.man.count(ctx.query);
  },

  /**
   * Create a/an man record.
   *
   * @return {Object}
   */

  create: async (ctx) => {
    return strapi.services.man.add(ctx.request.body);
  },

  /**
   * Update a/an man record.
   *
   * @return {Object}
   */

  update: async (ctx, next) => {
    return strapi.services.man.edit(ctx.params, ctx.request.body) ;
  },

  /**
   * Destroy a/an man record.
   *
   * @return {Object}
   */

  destroy: async (ctx, next) => {
    return strapi.services.man.remove(ctx.params);
  }
};
