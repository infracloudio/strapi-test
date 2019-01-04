'use strict';

/**
 * Woman.js controller
 *
 * @description: A set of functions called "actions" for managing `Woman`.
 */

module.exports = {

  /**
   * Retrieve woman records.
   *
   * @return {Object|Array}
   */

  find: async (ctx) => {
    if (ctx.query._q) {
      return strapi.services.woman.search(ctx.query);
    } else {
      return strapi.services.woman.fetchAll(ctx.query);
    }
  },

  /**
   * Retrieve a woman record.
   *
   * @return {Object}
   */

  findOne: async (ctx) => {
    if (!ctx.params._id.match(/^[0-9a-fA-F]{24}$/)) {
      return ctx.notFound();
    }

    return strapi.services.woman.fetch(ctx.params);
  },

  /**
   * Count woman records.
   *
   * @return {Number}
   */

  count: async (ctx) => {
    return strapi.services.woman.count(ctx.query);
  },

  /**
   * Create a/an woman record.
   *
   * @return {Object}
   */

  create: async (ctx) => {
    return strapi.services.woman.add(ctx.request.body);
  },

  /**
   * Update a/an woman record.
   *
   * @return {Object}
   */

  update: async (ctx, next) => {
    return strapi.services.woman.edit(ctx.params, ctx.request.body) ;
  },

  /**
   * Destroy a/an woman record.
   *
   * @return {Object}
   */

  destroy: async (ctx, next) => {
    return strapi.services.woman.remove(ctx.params);
  }
};
