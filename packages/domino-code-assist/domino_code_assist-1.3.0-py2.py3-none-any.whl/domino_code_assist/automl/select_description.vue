<template>
  <v-select :label="label" :items="items" v-model="value" hide_details="True">
    <template v-slot:item="{ item }">
      <v-list-item-content>
        <v-list-item-title>{{ item.text }}</v-list-item-title>
        <v-list-item-subtitle>{{ item.description }}</v-list-item-subtitle>
      </v-list-item-content>
    </template>
  </v-select>
</template>
