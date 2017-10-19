from pygame.sprite import RenderUpdates


class LayeredSpriteGroup(RenderUpdates):
    """..."""

    def __init__(self, sprite=()):
        RenderUpdates.__init__(self, sprite)
        self.orderedSprites = []

    def add_internal(self, sprite):
        # prevent duplication
        if sprite in self.spritedict:
            return

        RenderUpdates.add_internal(self, sprite)

        if not hasattr(sprite, 'zAxis'):
            # TODO: is this legal?
            sprite.zAxis = 0

        z = sprite.zAxis

        if z == 0:
            self.orderedSprites.insert(0, sprite)

        else:
            success = 0
            for i in range(len(self.orderedSprites) - 1):
                candidate = self.orderedSprites[i]
                if z < candidate.zAxis:
                    self.orderedSprites.insert(i, sprite)
                    success = 1
                    break
            if not success:
                self.orderedSprites.append(sprite)

    def remove_internal(self, sprite):
        RenderUpdates.remove_internal(self, sprite)
        self.orderedSprites.remove(sprite)

    def add(self, sprite):
        """add(sprite)
           add sprite to group

           Add a sprite or sequence of sprites to a group."""
        has = sprite in self.spritedict
        if hasattr(sprite, '_spritegroup'):
            for sprite in sprite.sprites():
                if not has:
                    self.add_internal(sprite)
                    sprite.add_internal(self)
        else:
            try:
                len(sprite)  # see if its a sequence
            except (TypeError, AttributeError):
                if not has:
                    self.add_internal(sprite)
                    sprite.add_internal(self)
            else:
                for sprite in sprite:
                    if not has:
                        self.add_internal(sprite)
                        sprite.add_internal(self)

    def add_top(self, sprite):
        """add_top(sprite)
           add sprite to group

           Add a sprite to a group above the highest z-axis level."""
        topsprite = self.orderedSprites[len(self.orderedSprites) - 1]
        z = topsprite.zAxis + 1
        sprite.zAxis = z

        self.add(sprite)

    def draw(self, surface):
        """draw(surface)
           draw all sprites onto the surface

           Draws all the sprites onto the given surface. It
           returns a list of rectangles, which should be passed
           to pygame.display.update()"""
        spritedict = self.spritedict
        surface_blit = surface.blit
        dirty = self.lostsprites
        dirty_append = dirty.append
        self.lostsprites = []
        for s in self.orderedSprites:
            r = spritedict[s]
            newrect = surface_blit(s.image, s.rect)
            if r is 0:
                dirty_append(newrect)
            else:
                if newrect.colliderect(r):
                    dirty_append(newrect.union(r))
                else:
                    dirty_append(newrect)
                    dirty_append(r)
            spritedict[s] = newrect
        return dirty

    def update(self, *args):
        """update(...)
           call update for all member sprites

           calls the update method for all sprites in the group.
           passes all arguments are to the Sprite update function.
           if a sprites' zAxis changes during its update(), the
           orderedSprites list is re sorted"""
        zBefore = 0
        dirty = 0
        if args:
            # a = apply
            for s in self.spritedict.keys():
                zBefore = s.zAxis
                # a(s.update, args)
                if zBefore != s.zAxis:
                    dirty = 1
        else:
            for s in self.spritedict.keys():
                zBefore = s.zAxis
                s.update()
                if zBefore != s.zAxis:
                    dirty = 1
        # if dirty:
            # fn = lambda x, y: cmp(x.zAxis, y.zAxis)
            # self.orderedSprites.sort(fn)