<template>
  <div>
    <v-menu v-model="opened" :close-on-content-click="false" >
      <template v-slot:activator="{ on }">
        <v-text-field :label="selected ? 'Experiment name' : 'Choose experiment'" readonly :value="selected" append-icon="mdi-menu-down" v-on="on" @click:append="opened=true"></v-text-field>
      </template>
      <v-sheet style="height: 50vh; max-height: 50vh;">
        <div v-if="loading" class="pa-4">
          <v-progress-linear indeterminate></v-progress-linear>
        </div>
        <div v-else style="display: flex; flex-direction: column; max-height: 100%">
          <div class="pa-2">
            <v-text-field label="Find or create experiment" hide-details v-model="search" autofocus></v-text-field>
          </div>
          <div style="flex-grow: 1; overflow: auto">
            <v-alert v-if="error" type="error">{{ error }}</v-alert>
            <v-list v-else>
              <v-list-item-group @change="set_selected">
                <v-list-item v-for="(item, index) in items" :key="item.name + index" :value="item.name">
                  <v-list-item-content>
                    <v-list-item-title>
                      <span v-for="(part, index) in split_name(item.name)" :key="index"
                            :style="part.toLowerCase() === (search && search.toLowerCase()) ? 'font-weight: bold' : ''">{{ part }}</span>
                    </v-list-item-title>
                    <v-list-item-subtitle>{{ item.description }}</v-list-item-subtitle>
                  </v-list-item-content>
                </v-list-item>
              </v-list-item-group>
            </v-list>
          </div>
          <v-btn text class="ma-2" v-if="search && !search_match" style="text-transform: unset"
                 @click="() => { selected = search }">
            <v-icon left>mdi-plus</v-icon>
            <span style="color: var(--jp-border-color1);">Create new experiment: </span>{{ search }}
          </v-btn>
        </div>
      </v-sheet>
    </v-menu>
  </div>
</template>
<script>
module.exports = {
  computed: {
    search_match() {
      return (this.items || []).filter(({name}) => name === this.search).length > 0;
    },
  },
  methods: {
    set_selected(v) {
      if (v != null) {
        this.selected = v;
      }
    },
    split_name(name) {
      if (!this.search) {
        return [name];
      }
      return name.split(new RegExp(`(${this.search})`, 'i'));
    },
  },
}
</script>
